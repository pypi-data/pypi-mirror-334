import datetime
from datetime import timezone

from sqlalchemy.orm import sessionmaker

from threatxmanager.base_module.base_module import BaseModule
from threatxmanager.dbmanager.modules_models.vendas import Venda


class SalesModule(BaseModule):
    """
    Sales Module.

    This module manages sales records in the "vendas" table. It provides functionality to register new sales
    and retrieve inserted sales records for demonstration purposes.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance inherited from BaseModule for logging messages.
    db_manager : DBManager
        Database manager instance inherited from BaseModule used to interact with the database.
    config : dict
        Module configuration loaded via BaseModule.
    info : dict
        Dictionary containing metadata about the module, such as name, description, author, license, and available actions.
    """

    def __init__(self, env: str | None = None) -> None:
        """
        Initialize the SalesModule.

        Parameters
        ----------
        env : str, optional
            Environment identifier for loading module-specific configuration.
            If None, the default environment from the configuration is used.
        """
        super().__init__(env=env)
        self.update_info(
            {
                "Name": "Sales Module",
                "Description": 'This module manages sales records in the "vendas" table.',
                "Author": ["Your Name"],
                "License": "MIT",
                "References": [["URL", "https://example.com/salesmodule"]],
                "Actions": [["RegisterSale", {"Description": "Register a new sale"}]],
                "DefaultAction": "RegisterSale",
            }
        )

    def run(self) -> None:
        """
        Execute the SalesModule functionalities.

        This method logs the execution process, loads both raw and obfuscated module configurations,
        and interacts with the database to create and retrieve a sales record.

        The following operations are performed:
            1. Log the start of module execution.
            2. Load module configuration and its obfuscated version.
            3. Create a new database session using the DBManager's engine.
            4. Create and add a new sales record with the current UTC date.
            5. Commit the transaction and log a success message.
            6. Retrieve the inserted sales record and log its details.
            7. Roll back and log an error message if an exception occurs.
            8. Close the database session.

        Raises
        ------
        Exception
            Propagates any exception encountered during database operations.
        """
        self.logger.info("Executing SalesModule functionalities.")
        module_config = self.load_module_config()
        safe_config = self.get_safe_module_config()
        self.logger.debug(f"Obfuscated module configuration: {safe_config}")
        self.logger.info(f"Loaded configuration: {module_config}")

        # Create a session factory using the engine from the DBManager.
        session_factory = sessionmaker(bind=self.db_manager.get_engine())
        session = session_factory()
        try:
            # Create a new sales record using the current UTC date.
            new_sale = Venda(
                sale_date=datetime.datetime.now(timezone.utc).date(),
                customer="Example Customer",
                product="Product X",
                quantity=10,
                unit_price=25.50,
            )
            session.add(new_sale)
            session.commit()
            self.logger.info("Sales record inserted successfully.")

            # Retrieve the inserted record for demonstration purposes.
            sale_record = session.query(Venda).filter_by(id=new_sale.id).first()
            self.logger.info(f"Retrieved sales record: {sale_record}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error registering sale: {e}")
            raise
        finally:
            session.close()
            self.logger.debug("Database session closed.")
