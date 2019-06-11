import { connect } from 'react-redux';
import React, { Component } from 'react';

import { Icon, Position, Tooltip, Tree } from "@blueprintjs/core";

import { datasets } from "../../actions";

// https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
class DatasetTree extends Component {
  state = {
    selectedProjectId: null,
    selectedProjectName: 'Projects',
  }

  // componentDidMount() {
  //   this.props.fetchDatasets();
  // }

  items(){
    return(this.props.datasets);
  }

  nodes(){
    var nodes = [];
    for(var i=0;i<this.items().length;i++) {
      nodes.push({
        id: this.items()[i].id,
        hasCaret: true,
        icon: "folder-close",
        label: this.items()[i].name,
      })
    }
    return nodes;
    
    return [
        {
            id: 0,
            hasCaret: true,
            icon: "folder-close",
            label: "Folder 0",
        },
        {
            id: 1,
            icon: "folder-close",
            isExpanded: true,
            label: (
                <Tooltip content="I'm a folder <3" position={Position.RIGHT}>
                    Folder 1
                </Tooltip>
            ),
            childNodes: [
                {
                    id: 2,
                    icon: "document",
                    label: "Item 0",
                    secondaryLabel: (
                        <Tooltip content="An eye!">
                            <Icon icon="eye-open" />
                        </Tooltip>
                    ),
                },
                {
                    id: 3,
                    icon: "tag",
                    label: "Organic meditation gluten-free, sriracha VHS drinking vinegar beard man.",
                },
                {
                    id: 4,
                    hasCaret: true,
                    icon: "folder-close",
                    label: (
                        <Tooltip content="foo" position={Position.RIGHT}>
                            Folder 2
                        </Tooltip>
                    ),
                    childNodes: [
                        { id: 5, label: "No-Icon Item" },
                        { id: 6, icon: "tag", label: "Item 1" },
                        {
                            id: 7,
                            hasCaret: true,
                            icon: "folder-close",
                            label: "Folder 3",
                            childNodes: [
                                { id: 8, icon: "document", label: "Item 0" },
                                { id: 9, icon: "tag", label: "Item 1" },
                            ],
                        },
                    ],
                },
            ],
        },
    ];
  }

  render() {
    return(
      <Tree
        contents={this.nodes()}
        // onNodeClick={this.handleNodeClick}
        // onNodeCollapse={this.handleNodeCollapse}
        // onNodeExpand={this.handleNodeExpand}
        // className={Classes.ELEVATION_0}
      />
    );
  }
}

const mapStateToProps = state => {
  return {
    datasets: state.datasets,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    fetchDatasets: () => {
      dispatch(datasets.fetchDatasets());
    }
  }
}
export default (DatasetTree);
// export default connect(mapStateToProps, mapDispatchToProps)(DatasetTree);
