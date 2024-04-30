export type GlobalVariablesStore = {
  globalVariablesEntries: Array<string>;
  globalVariables: { [name: string]: { id: string; type?: string } };
  setGlobalVariables: (variables: {
    [name: string]: { id: string; type?: string };
  }) => void;
  addGlobalVariable: (name: string, id: string, type?: string) => void;
  removeGlobalVariable: (name: string) => void;
  getVariableId: (name: string) => string | undefined;
  avaliableFields: Set<string>;
  setAvaliableFields: (fields: Set<string>) => void;
  addAvaliableField: (field: string) => void;
  unavaliableFields: Set<string>;
  setUnavaliableFields: (fields: Set<string>) => void;
  addUnavaliableField: (field: string) => void;
  removeUnavaliableField: (field: string) => void;
};
