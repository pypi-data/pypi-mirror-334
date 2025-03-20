from .frog_data import FrogModel
from .frog_activity import activity_signal

import json
from typing import List, Union, Dict, Any

SCENARIO_COLUMN_NAME = "scenarioname"
SCENARIO_INPUT_TABLES = ["scenarios", "scenarioitemassignments"]

# TODO
# what about rules?

class ScenarioHelper:
    def __init__(self, model: FrogModel, delete_outputs=False, delete_inputs=False, send_signals=False, print_informative_logs=False):
        self.delete_outputs = delete_outputs
        self.delete_inputs = delete_inputs
        self.send_signals = send_signals
        self.print_informative_logs = print_informative_logs
        self.model = model

    def delete_scenarios(self, scenario_names: List[str]) -> dict[str, Union[bool, str]]:
        """
        Deletes multiple scenarios from the database.
        """

        if len(scenario_names) == 0:
            if self.print_informative_logs:
                print("No scenario names provided.")
            return { "success": False, "message": "Provide scenario names to delete."}
        
        if not self.delete_outputs and not self.delete_inputs:
            if self.print_informative_logs:
                print("Nothing to delete.")
            return { "success": False, "message": "Nothing to delete, have to provide delete_outputs or delete_inputs as True."}
        
        delete_statements = []

        try:
            scenario_names_for_query = "('" + "', '".join(scenario_names) + "')"

            if self.delete_outputs:
                self.delete_output_data(delete_statements, scenario_names_for_query)
            
            if self.delete_inputs:
                self.delete_input_data(delete_statements, scenario_names_for_query)

            self.model.exec_sql(';'.join(delete_statements))

            self.update_maps(scenario_names)

            if self.send_signals:
                self.fire_signals()

            if self.print_informative_logs:
                print("Scenarios deleted!")
                print("Deleting scenario from Maps if selected...")

            return { "success": True, "message": "Scenarios deleted!" }
        except Exception as e:
            return { "success": False, "message": f"Error deleting scenarios: {str(e)}" }

    def delete_statement_multiple(self, scenario_names: str, table_name: str) -> str:
        return f"DELETE FROM {table_name} WHERE scenarioname in {scenario_names}"

    def delete_output_data(self, delete_statements: List[str], scenario_name: str) -> List[str]:
        output_table_names = self.model.get_tablelist(output_only=True)

        if self.print_informative_logs:
            print("Output table names: ", output_table_names)
        for table_name in output_table_names:
            column_names = self.model.get_columns(table_name)
            if SCENARIO_COLUMN_NAME in column_names:
                query = self.delete_statement_multiple(scenario_name, table_name)
                delete_statements.append(query)
                if self.print_informative_logs:
                    print("Deleting from table: ", table_name)
                    print(query)

        return delete_statements

    def delete_input_data(self, delete_statements: List[str], scenario_name: str) -> List[str]:
        for table_name in SCENARIO_INPUT_TABLES:
            query = self.delete_statement_multiple(scenario_name, table_name)
            delete_statements.append(query)
            if self.print_informative_logs:
                print("Deleting from table: ", table_name)
                print(query)
        
        return delete_statements

    def send_signal(self, message: Dict[str, Any], topic: str):
        activity_signal(
            self.model.log,
            message=message,
            app_key=self.model._app_key,
            model_name=self.model.model_name,
            signal_topic=topic
        )
    
    def fire_signals(self):
        self.send_signal({"type": "category","categoryName": "output"}, "REFRESH COUNT")
        self.send_signal({}, "REFETCH SCENARIO ERRORS")
        self.send_signal({}, "REFETCH SCENARIOS") # TODO: How will this look when scenario screen gets scalable?
        self.send_signal({}, "REFETCH MAPS")

    def update_maps(self, scenario_names: List[str]):
        maps = self.model.read_table("maps")
        for _, row in maps.iterrows():      
            # Check if 'data' field is a string
            if isinstance(row["data"], str):
                try:
                    data = json.loads(row["data"])
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for map {row['mapname']}: {e}")
                    continue
                
                # Check if data is a dictionary
                if isinstance(data, dict):
                    if data.get("scenarioName") in scenario_names:
                        data["scenarioName"] = "Baseline"
                        if self.print_informative_logs:
                            print("Updating map: ", row["mapname"])
                        try:
                            json_data = json.dumps(data).replace("'", "''")
                            self.model.exec_sql(f"UPDATE maps SET data = '{json_data}' WHERE mapname = '{row['mapname']}'")
                        except Exception as e:
                            print(f"Error updating map {row['mapname']}: {e}")
                else:
                    print(f"Unexpected data type for map {row['mapname']}: {type(data)}")
            else:
                print(f"Missing or invalid 'data' field for map {row['mapname']}")
