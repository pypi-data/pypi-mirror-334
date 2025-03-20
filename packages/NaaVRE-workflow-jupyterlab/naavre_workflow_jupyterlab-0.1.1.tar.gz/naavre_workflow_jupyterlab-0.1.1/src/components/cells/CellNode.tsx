import React, { useEffect, useState } from 'react';
import { REACT_FLOW_CHART } from '@mrblenny/react-flow-chart';

import { ICell } from '../../naavre-common/types/NaaVRECatalogue/WorkflowCells';
import { ISpecialCell } from '../../utils/specialCells';
import { cellToChartNode } from '../../utils/chart';

export function CellNode({
  cell,
  setSelectedCellInList
}: {
  cell: ICell | ISpecialCell;
  setSelectedCellInList: (c: ICell | null) => void;
}) {
  const [selected, setSelected] = useState(false);

  useEffect(() => {
    setSelectedCellInList(selected ? cell : null);
  }, [selected]);

  const node = cellToChartNode(cell);
  const is_special_node = node.type !== 'workflow-cell';

  return (
    <div
      onMouseEnter={() => setSelected(true)}
      onMouseLeave={() => setSelected(false)}
      draggable={true}
      onDragStart={(event: any) => {
        event.dataTransfer.setData(
          REACT_FLOW_CHART,
          JSON.stringify({
            type: node.type,
            ports: node.ports,
            properties: node.properties
          })
        );
      }}
      style={{
        margin: '10px',
        fontSize: '14px',
        display: 'flex',
        height: '35px',
        border: '1px solid lightgray',
        justifyContent: 'center',
        alignItems: 'center',
        background: 'rgb(195, 235, 202)',
        backgroundColor: is_special_node
          ? 'rgb(195, 235, 202)'
          : 'rgb(229,252,233)',
        borderRadius: '5px',
        padding: '5px'
      }}
    >
      <span
        style={{
          textAlign: 'center',
          overflow: 'hidden',
          textOverflow: 'ellipsis'
        }}
      >
        {cell.title}
      </span>
    </div>
  );
}
