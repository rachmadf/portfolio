from repositories.store_repository import StoreRepository
from models.store_models import Store


class StoreService:

    # ======================================================
    # Get All Stores
    # ======================================================
    @staticmethod
    def get_all():

        return StoreRepository.get_all()


    # ======================================================
    # Get Store By ID
    # ======================================================
    @staticmethod
    def get_by_id(store_id: int):

        return StoreRepository.get_by_id(store_id)


    # ======================================================
    # Check Store Name Exists
    # ======================================================
    @staticmethod
    def exists_by_name(store_name: str):

        return StoreRepository.exists_by_name(store_name)


    # ======================================================
    # Create Store
    # ======================================================
    @staticmethod
    def create(store: Store):

        if StoreRepository.exists_by_name(store.store_name):
            raise ValueError("Store name already exists.")

        return StoreRepository.insert(store)


    # ======================================================
    # Update Store
    # ======================================================
    @staticmethod
    def update(store: Store):

        existing = StoreRepository.get_by_id(store.store_id)

        if existing is None:
            raise ValueError("Store not found.")

        return StoreRepository.update(store)


    # ======================================================
    # Delete Store
    # ======================================================
    @staticmethod
    def delete(store_id: int):

        existing = StoreRepository.get_by_id(store_id)

        if existing is None:
            raise ValueError("Store not found.")

        return StoreRepository.delete(store_id)