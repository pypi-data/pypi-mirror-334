import { NaaVREExternalService } from '../naavre-common/handler';
import { ICell } from '../naavre-common/types/NaaVRECatalogue/WorkflowCells';

export async function getCellsFromCatalogue(
  catalogueServiceUrl: string
): Promise<Array<ICell>> {
  const resp = await NaaVREExternalService(
    'GET',
    `${catalogueServiceUrl}/workflow-cells/`,
    {
      accept: 'application/json'
    }
  );
  if (resp.status_code !== 200) {
    throw `${resp.status_code} ${resp.reason}`;
  }
  return JSON.parse(resp.content).results;
}
