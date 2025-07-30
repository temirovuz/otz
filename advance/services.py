

from decimal import Decimal
from advance.models import Advance

class AdvanceSettlementService:
    @staticmethod
    def settle_advances(user, amount):
        if not user or not amount or amount <= 0:
            return

        unpaid_advances = Advance.objects.filter(employee=user, is_settled=False).order_by('id')
        remaining_amount = Decimal(amount)

        for advance in unpaid_advances:
            if remaining_amount <= 0:
                break

            if remaining_amount >= advance.settled_amount:
                remaining_amount -= advance.settled_amount
                advance.settled_amount = Decimal('0')
                advance.is_settled = True
            else:
                advance.settled_amount -= remaining_amount
                remaining_amount = Decimal('0')

            advance.save(update_fields=['settled_amount', 'is_settled'])
