
from datetime import date
from dataclasses import dataclass

from inoopa_utils.custom_types.addresses import Country


@dataclass(slots=True)
class PerEmployeeCategory:
    """Hold the counting of a metric."""
    total: int | None = None
    distinct: int | None = None
    emp_0: int = 0
    emp_1_to_4: int = 0
    emp_5_to_10: int = 0
    emp_10_to_19: int = 0
    emp_20_to_49: int = 0
    emp_50_to_99: int = 0
    emp_100_to_199: int = 0
    emp_200_to_499: int = 0
    emp_500_to_999: int = 0
    emp_1000_plus: int = 0
    unknown: int = 0


@dataclass(slots=True)
class CompanyStats:
    """
    Hold the metrics of our company collection at a given point in time.
    Each metric is divided by employee category.
    """
    date: date
    country: Country
    active_companies: PerEmployeeCategory 
    websites: PerEmployeeCategory 
    emails: PerEmployeeCategory
    phones: PerEmployeeCategory 
    attributed_phones: PerEmployeeCategory 


@dataclass(slots=True)
class DecisionMakersStats:
    """
    Hold the stats of the decision_makers collection at a given point in time.
    Each metric is divided by employee category.
    """
    date: date
    country: Country
    with_name: PerEmployeeCategory
    with_job_title: PerEmployeeCategory
    with_department: PerEmployeeCategory
    with_responsibility_level: PerEmployeeCategory
    with_linkedin_url: PerEmployeeCategory
    with_email: PerEmployeeCategory


def dict_to_company_stats(company_stats: dict) -> CompanyStats:
    """Convert a dict from the DB to a CompanyStats dataclass."""
    company_stats_fmt = CompanyStats(
        date=company_stats["date"],
        country=Country(company_stats["country"]),
        active_companies=PerEmployeeCategory(**company_stats["active_companies"]),
        websites=PerEmployeeCategory(**company_stats["websites"]),
        phones=PerEmployeeCategory(**company_stats["phones"]),
        emails=PerEmployeeCategory(**company_stats["emails"]),
        attributed_phones=PerEmployeeCategory(**company_stats["attributed_phones"]),
    )
    return company_stats_fmt


def dict_to_decision_makers_stats(decision_makers_stats: dict) -> DecisionMakersStats:
    """Convert a dict from the DB to a DecisionMakersStats dataclass."""
    decision_makers_stats_fmt = DecisionMakersStats(
        date=decision_makers_stats["date"],
        country=Country(decision_makers_stats["country"]),
        with_name=PerEmployeeCategory(**decision_makers_stats["with_name"]),
        with_job_title=PerEmployeeCategory(**decision_makers_stats["with_job_title"]),
        with_department=PerEmployeeCategory(**decision_makers_stats["with_department"]),
        with_responsibility_level=PerEmployeeCategory(**decision_makers_stats["with_responsibility_level"]),
        with_linkedin_url=PerEmployeeCategory(**decision_makers_stats["with_linkedin_url"]),
        with_email=PerEmployeeCategory(**decision_makers_stats["with_email"]),
    )
    return decision_makers_stats_fmt

