from datetime import date

from database.models import db

from database.warehouse import (
    DimUser,
    DimDate,
    FactDailyHealth
)


def get_date_dimension():

    today = date.today()

    dim = DimDate.query.filter_by(
        full_date=today
    ).first()

    if dim:
        return dim

    dim = DimDate(

        full_date=today,

        day=today.day,

        month=today.month,

        year=today.year,

        weekday=today.strftime("%A"),

        month_name=today.strftime("%B")

    )

    db.session.add(dim)

    db.session.commit()

    return dim


def load_data(warehouse_data):

    dim_date = get_date_dimension()

    for row in warehouse_data:

        user = row["user"]

        profile = row["profile"]

        progress = row["progress"]

        dim_user = DimUser.query.filter_by(
            user_id=user.id
        ).first()

        if not dim_user:

            dim_user = DimUser(

                user_id=user.id,

                name=user.name,

                age=profile.age if profile else None,

                gender=profile.gender if profile else None,

                goal=profile.goal if profile else None,

                activity_level=profile.activity_level if profile else None

            )

            db.session.add(dim_user)

            db.session.commit()

        fact = FactDailyHealth(

            user_key=dim_user.user_key,

            date_key=dim_date.date_key,

            weight=progress.weight_kg if progress else None,

            bmi=progress.bmi if progress else None,

            calories=progress.calories if progress else None,

            health_score=row["health_score"]

        )

        db.session.add(fact)

    db.session.commit()

    print("ETL Load Completed Successfully")