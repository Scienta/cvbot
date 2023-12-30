import logging
from typing import List, Callable, TypeVar, Optional

from scienta import cvpartner_api
from scienta.cvpartner_api import CvListEntry

logger = logging.getLogger(__name__)
T = TypeVar("T")


class CvPartnerClient:
    def __init__(self, client: cvpartner_api.DefaultApi):
        self.client = client

    def find_office_ids(self):
        countries = self.client.find_countries()
        # print("countries")
        # print(countries)

        ids = []
        for country in countries:
            for office in country.offices:
                ids.append(office.id)

        return ids

    def find_cvs(self, office_ids: List[str], max_len=None) -> List[CvListEntry]:
        page_size = 100
        remaining = None
        items = []
        while True:
            offset = len(items)

            logger.info(f"Fetching page {1 + offset / page_size}")
            req = cvpartner_api.SearchByNameReq.from_dict({
                "offset": offset,
                "size": page_size,
                "office_ids": office_ids,
                "must": {},
            })
            res = self.client.search_by_name(search_by_name_req=req)

            if remaining is None:
                logger.info("There are {} CVs", res.total)
                remaining = res.total

            items.extend(res.cvs)
            remaining -= len(res.cvs)

            if remaining <= 0:
                break

            if max_len is not None and len(items) >= max_len:
                break

        return items

    def user_search(self, name: Optional[str] = None) -> List[cvpartner_api.User]:
        def fetch_page(offset: int, page_size: int) -> List[cvpartner_api.User]:
            logger.info(f"Fetching users {offset}-{offset + page_size}")
            return self.client.user_search(var_from=offset, size=page_size,
                                           name=name)

        return self.foreach_page(10, fetch_page)

    @staticmethod
    def foreach_page(page_size: int, callback: Callable[[int, int], List[T]]) -> List[T]:
        lst = []
        offset = 0
        while True:
            res = callback(offset, page_size)
            if len(res) == 0:
                break
            offset += page_size
            lst.extend(res)

        return lst
