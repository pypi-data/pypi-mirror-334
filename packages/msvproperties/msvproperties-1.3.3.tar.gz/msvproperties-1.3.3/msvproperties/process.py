from .api import API
from .logger import ProcessLogger
from .config import get_config


class ProcessLogic:
    def __init__(self, data, session, force=False):
        LOG_PATH, _, _, _ = get_config()
        self.logger = ProcessLogger(LOG_PATH)
        self.DATA = data
        self.session = session
        self.force = force
        session.authenticate()

    def log_failure(self, cause, message=""):
        self.logger.log_failure(
            address=self.DATA.property.address,
            cause=cause,
            source_name=self.DATA.property.source_name,
            is_auction=self.DATA.property.is_auction,
            user=self.session.username,
        )
        return False

    def initial_layer(self):
        if self.DATA.property.is_auction:
            return True

        def check_and_log_difference(value_diff, message):
            if value_diff < 40000:
                return self.log_failure(f"{message} difference < 40000 (initial layer)")
            return True

        property_data = self.DATA.property
        auction = property_data.auctions[0]
        legal_proceeding = property_data.legal_proceedings[0]
        sale = property_data.sales[0]

        if all(
            [
                auction.amount,
                legal_proceeding.final_judgment,
            ]
        ):
            auction_diff = auction.amount - legal_proceeding.final_judgment
            if not check_and_log_difference(
                auction_diff, "Auction value and final judgment"
            ):
                return False

        if all([sale.sale_amount, auction.opening_bid]):
            sold_diff = sale.sale_amount - auction.opening_bid
            if not check_and_log_difference(sold_diff, "Sold value and opening bid"):
                return False
        return True

    def zillow_layer(self):
        if not self.DATA.property.is_auction:
            return self.DATA.property

        exclude_status = {
            "SOLD",
            "OTHERS",
            "RECENTLY_SOLD",
            "FOR_SALE",
            "ACTIVE",
            "PENDING",
            "FOR_RENT",
        }

        property_data = self.DATA.property
        zestimate_low = property_data.zestimate_low
        auction = property_data.auctions[0]
        legal_proceeding = property_data.legal_proceedings[0]

        if not zestimate_low:
            return True

        if property_data.status in exclude_status:
            return self.log_failure(
                f"Status {property_data.status} is in exclude_status list (zillow layer)"
            )

        if zestimate_low <= 150000:
            return self.log_failure(
                f"Zestimate low {zestimate_low} <= 150,000 (zillow layer)"
            )

        opening_bid = auction.opening_bid
        if opening_bid and opening_bid >= 0.50 * zestimate_low:
            return self.log_failure(
                f"Opening bid {opening_bid} >= 50% of Zestimate low {zestimate_low} (zillow layer)"
            )

        total_amount_owed = legal_proceeding.total_amount_owed
        if total_amount_owed:
            if total_amount_owed >= 0.50 * zestimate_low:
                return self.log_failure(
                    f"Total amount owed {total_amount_owed} >= 50% of Zestimate low {zestimate_low} (zillow layer)"
                )
            if zestimate_low - total_amount_owed < 100000:
                return self.log_failure(
                    f"Difference between Zestimate low and total amount owed "
                    f"({zestimate_low - total_amount_owed}) < 100,000 (zillow layer)"
                )

        return True

    def propstream_layer(self):
        property_data = self.DATA.property
        debt = property_data.debts[0]
        auction = property_data.auctions[0]
        legal_proceeding = property_data.legal_proceedings[0]
        sale = property_data.sales[0]

        if debt.amount:
            debt.type = "debt provided in website"

        if property_data.owners:
            last_name = property_data.owners[0].get("last_name", "").lower()
            excluded_last_names = {
                "construction",
                "bank",
                "developers",
                "land",
                "corporation",
                "holdings",
            }
            if any(excluded_name in last_name for excluded_name in excluded_last_names):
                return self.log_failure(
                    f"Excluded due to last name '{last_name}' (propstream layer)"
                )

        property_type = (
            property_data.property_type.lower() if property_data.property_type else ""
        )
        excluded_property_types = {
            "vacant",
            "mobile",
            "rural residence",
            "public school",
            "farm land",
        }
        if any(
            excluded_type in property_type for excluded_type in excluded_property_types
        ):
            return self.log_failure(
                f"Excluded due to property type '{property_type}' (propstream layer)"
            )

        if property_data.is_auction:
            opening_bid = auction.opening_bid
            final_judgment = legal_proceeding.final_judgment

            if (
                all([opening_bid, final_judgment])
                and max(opening_bid, final_judgment) > 1000
            ):
                debt.amount = max(opening_bid, final_judgment)
                debt.type = "maximum value of opening bid and final judgment"

            est_remaining_balance = property_data.est_remaining_balance
            if est_remaining_balance and not debt.amount:
                debt.amount = est_remaining_balance
                debt.type = "est remaining balance"

            if all([debt.amount, property_data.zestimate_low]):
                zestimate_low = property_data.zestimate_low
                if debt.amount >= 0.50 * zestimate_low:
                    return self.log_failure(
                        f"Max debt {debt.amount} >= 50% of Zestimate low {zestimate_low} (propstream layer)"
                    )
                if zestimate_low - debt.amount <= 100000:
                    return self.log_failure(
                        f"Zestimate low - Max debt <= 100,000 (propstream layer)"
                    )
        else:
            sale_amount = sale.sale_amount
            est_remaining_balance = property_data.est_remaining_balance
            if all([sale_amount, est_remaining_balance]):
                if sale_amount - est_remaining_balance < 40000:
                    return self.log_failure(
                        f"Sold value {sale_amount} - Estimated remaining balance {est_remaining_balance} < 40,000 (propstream layer)"
                    )

        return True

    def start(self):

        if not self.force:
            if not self.initial_layer():
                return False, "Removed by initial filters"

        api = API(self.session, self.DATA.property)

        print(f"{self.DATA.property.address}: Starting Zillow Batching")
        zillow_output = api.get_zillow_output(self.DATA.property.address)
        if not zillow_output:
            return self.DATA, "Zillow Response is None"
        self.update_property_data(zillow_output)

        if not self.force:
            if not self.zillow_layer():
                return False, "Removed by Zillow filters"

        print(f"{self.DATA.property.address}: Starting Propstream Batching")
        propstream_output = api.get_propstream_output(self.DATA.property.address)

        if not propstream_output:
            return self.DATA, "Propstream Response is None"

        self.update_property_data(propstream_output)
        if not self.force:
            if not self.propstream_layer():
                return False, "Removed by Propstream filters"

        print(f"{self.DATA.property.address}: Starting Tracers Batching")
        setattr(self.DATA.property, "related_people", self.get_tracers_data(api))

        return self.DATA, "Process is done"

    def update_property_data(self, new_data):
        for key, value in new_data.items():
            property_key = getattr(self.DATA.property, key, None)
            if isinstance(property_key, list):
                property_key += value
            elif not property_key :
                setattr(self.DATA.property, key, value)

    def get_tracers_data(self, api):
        tracers_results = []
        for owner in self.DATA.property.owners:
            tracers_output = api.get_tracer_output(
                owner.get("first_name"),
                owner.get("middle_name"),
                owner.get("last_name"),
                self.DATA.property.propstream_address,
                self.DATA.property.propstream_city,
                self.DATA.property.propstream_state,
                self.DATA.property.propstream_zip,
            )
            if tracers_output:
                tracers_results += tracers_output
        return tracers_results
