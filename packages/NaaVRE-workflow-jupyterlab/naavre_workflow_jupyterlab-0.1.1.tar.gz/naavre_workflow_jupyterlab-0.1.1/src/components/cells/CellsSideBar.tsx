import React, { useEffect, useState } from 'react';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Tooltip from '@mui/material/Tooltip';
import RefreshIcon from '@mui/icons-material/Refresh';

import { ICell } from '../../naavre-common/types/NaaVRECatalogue/WorkflowCells';
import { specialCells } from '../../utils/specialCells';
import { getCellsFromCatalogue } from '../../utils/catalog';
import { CellsList } from './CellsList';

export function CellsSideBar({
  catalogueServiceUrl,
  setSelectedCellInList
}: {
  catalogueServiceUrl: string | undefined;
  setSelectedCellInList: (c: ICell | null) => void;
}) {
  const [catalogItems, setCatalogItems] = useState<Array<ICell>>([]);

  const getCatalogItems = () => {
    if (catalogueServiceUrl) {
      getCellsFromCatalogue(catalogueServiceUrl).then(cells => {
        setCatalogItems(cells);
      });
    }
  };

  useEffect(() => getCatalogItems(), [catalogueServiceUrl]);

  return (
    <Paper
      elevation={12}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 250,
        height: '100%',
        overflowX: 'hidden',
        overflowY: 'scroll',
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 0
      }}
    >
      <CellsList
        title="Cells Catalog"
        cells={catalogItems}
        style={{ flexGrow: 1 }}
        setSelectedCellInList={setSelectedCellInList}
        button={
          <Tooltip title="Refresh" arrow>
            <IconButton
              aria-label="Reload"
              style={{ color: 'white' }}
              onClick={getCatalogItems}
            >
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        }
      />
      <CellsList
        title="Special cells"
        cells={specialCells}
        setSelectedCellInList={setSelectedCellInList}
      />
    </Paper>
  );
}
