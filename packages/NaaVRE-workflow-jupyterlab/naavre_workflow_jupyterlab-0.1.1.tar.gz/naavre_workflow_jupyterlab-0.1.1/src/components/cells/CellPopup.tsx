import React from 'react';
import Paper from '@mui/material/Paper';

import { CellInfo } from '../common/CellInfo';
import { ICell } from '../../naavre-common/types/NaaVRECatalogue/WorkflowCells';

export function CellPopup({ cell }: { cell: ICell }) {
  return (
    <Paper
      elevation={12}
      sx={{
        position: 'absolute',
        top: 20,
        left: 'calc(20px + 250px)',
        width: 380,
        maxHeight: 'calc(100% - 40px)',
        overflowX: 'clip',
        overflowY: 'scroll'
      }}
    >
      <p className="naavre-workflow-section-header">{cell.title}</p>
      <CellInfo cell={cell} />
    </Paper>
  );
}
