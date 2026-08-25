from django.db import transaction

from shared.masked_and_pattern.masked import (
    mask_address,
    mask_credit_card,
    mask_dob,
    mask_email,
    mask_phone_number,
)

from ..queries.masking_data_queries import get_masking_data_by_id, update_masking_data

MASKED_BY_FIELD = {
    'email': 'masked_email',
    'phone_number': 'masked_phone_number',
    'dob': 'masked_dob',
    'address': 'masked_address',
}

MASK_BY_FIELD = {
    'email': mask_email,
    'phone_number': mask_phone_number,
    'dob': mask_dob,
    'address': mask_address,
}


def update_masking_data_service(masking_data_id, validated_data):
    instance = get_masking_data_by_id(masking_data_id)

    fields = {}
    for field, mask_fn in MASK_BY_FIELD.items():
        if field in validated_data:
            fields[field] = validated_data[field]
            fields[MASKED_BY_FIELD[field]] = mask_fn(validated_data[field])

    with transaction.atomic():
        update_masking_data(instance, **fields)
        if 'credit_card' in validated_data:
            update_masking_data(
                instance.credit_card,
                number=validated_data['credit_card'],
                masked_number=mask_credit_card(validated_data['credit_card']),
            )

    return instance
