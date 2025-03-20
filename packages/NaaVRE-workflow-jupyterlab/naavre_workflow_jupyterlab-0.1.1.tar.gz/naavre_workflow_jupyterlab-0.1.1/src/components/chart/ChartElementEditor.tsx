import * as React from 'react';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import {
  IChart,
  IConfig,
  IFlowChartCallbacks,
  ILink,
  INode
} from '@mrblenny/react-flow-chart';

import { CellInfo } from '../common/CellInfo';

function LinkEditor({ link }: { link: ILink }) {
  return (
    <>
      <p className="naavre-workflow-section-header">Link</p>
    </>
  );
}

function NodeEditor({ node }: { node: INode }) {
  let title: string = '';
  switch (node.type) {
    case 'splitter':
      title = 'Splitter';
      break;
    case 'merger':
      title = 'Merger';
      break;
    case 'visualizer':
      title = 'Visualizer';
      break;
    case 'workflow-cell':
      title = node.properties.cell.title;
      break;
  }

  return (
    <>
      <p className="naavre-workflow-section-header">{title}</p>
      {node.type === 'workflow-cell' && (
        <CellInfo cell={node.properties.cell} />
      )}
    </>
  );
}

export function ChartElementEditor({
  chart,
  callbacks,
  config
}: {
  chart: IChart;
  callbacks: IFlowChartCallbacks;
  config: IConfig;
}) {
  // when no chart element is selected, chart.selected === {}
  if (!chart.selected.id) {
    return <></>;
  }

  return (
    <Paper
      elevation={6}
      sx={{
        position: 'absolute',
        top: 20,
        right: 20,
        width: 380,
        maxHeight: 'calc(100% - 40px)',
        overflowX: 'clip',
        overflowY: 'scroll'
      }}
    >
      {chart.selected.type === 'link' && (
        <LinkEditor link={chart.links[chart.selected.id as string]} />
      )}
      {chart.selected.type === 'node' && (
        <NodeEditor node={chart.nodes[chart.selected.id as string]} />
      )}
      <div style={{ margin: '15px' }}>
        <Button
          variant="contained"
          onClick={() => {
            return callbacks.onDeleteKey({ config: config });
          }}
        >
          Delete
        </Button>
      </div>
    </Paper>
  );
}
