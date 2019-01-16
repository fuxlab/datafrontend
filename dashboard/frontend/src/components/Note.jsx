import React, { Component } from 'react';
import {connect} from 'react-redux';
import {notes} from "../actions";

import {
    Icon,
    Button,
    InputGroup,
} from "@blueprintjs/core";

import Menu from "./base/Menu";
import EditWindow from "./base/EditWindow";

class Note extends Component {

  state = {
    text: "",
    updateNoteId: null,
  }

  resetForm = () => {
    this.setState({text: "", updateNoteId: null});
  }

  selectForEdit = (id) => {
    this.refs.EditNoteWindow.setState({ isOpen: true});
    let note = this.props.notes[id];
    this.setState({text: note.text, updateNoteId: id});
  }

  submitNote = (e) => {
    if(e) {
      e.preventDefault();
    }
    if (this.state.updateNoteId === null) {
      this.props.addNote(this.state.text).then(this.resetForm)
    } else {
      this.props.updateNote(this.state.updateNoteId, this.state.text);
    }
  }
  
  toggleEditForm(){
    this.refs.EditNoteWindow.setState({ isOpen: true});
  }

  componentDidMount() {
    this.props.fetchNotes();
  }

  render() {
    return (
      <div>
        <Menu />
        <Button icon="add" text="Show" onClick={() => this.toggleEditForm()} />

        <h2><Icon icon="document" /> Notes</h2>
        <hr />
        <EditWindow title="Edit Note" ref="EditNoteWindow" icon="box" submitMethod={this.submitNote}>
          <form ref="form" onSubmit={this.submitNote}>
            <InputGroup
                large="true"
                value={this.state.text}
                placeholder="Enter note here..."
                onChange={(e) => this.setState({text: e.target.value})}
                required            
            />
          </form>
        </EditWindow>
        
        <h3>Notes</h3>

        <table className="bp3-html-table bp3-html-table-bordered bp3-interactive" width="100%">
          <tbody>
            {this.props.notes.map((note, id) => (
              <tr key={`note_${id}`}>
                <td>{note.id}</td>
                <td>{note.text}</td>
                <td>
                  <button onClick={() => this.selectForEdit(id)}>edit</button>
                  <button onClick={() => this.props.deleteNote(id)}>delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }
}

const mapStateToProps = state => {
  return {
    notes: state.notes,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    deleteNote: (id) => {
      dispatch(notes.deleteNote(id));
    },
    fetchNotes: () => {
      dispatch(notes.fetchNotes());
    },
    addNote: (text) => {
      return dispatch(notes.addNote(text));
    },
    updateNote: (id, text) => {
      return dispatch(notes.updateNote(id, text));
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Note);