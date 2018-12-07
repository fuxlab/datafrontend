import React, { Component } from 'react';
import {connect} from 'react-redux';
import {notes} from "../actions";


import {
    Icon,
    Button,
    InputGroup,
} from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import Menu from "./Menu";

class Note extends Component {

  state = {
    text: "",
    updateNoteId: null,
  }

  resetForm = () => {
    this.setState({text: "", updateNoteId: null});
  }

  selectForEdit = (id) => {
    let note = this.props.notes[id];
    this.setState({text: note.text, updateNoteId: id});
  }

  submitNote = (e) => {
    e.preventDefault();
    if (this.state.updateNoteId === null) {
      this.props.addNote(this.state.text).then(this.resetForm)
    } else {
      this.props.updateNote(this.state.updateNoteId, this.state.text);
    }
  }
  
  componentDidMount() {
    this.props.fetchNotes();
  }

  render() {
    return (
      <div>
        <Menu />

        <h2><Icon icon="document" /> Notes</h2>
        <hr />
        
        <h3>Add new note</h3>
        
        <form onSubmit={this.submitNote}>
          <InputGroup
              large="true"
              value={this.state.text}
              placeholder="Enter note here..."
              onChange={(e) => this.setState({text: e.target.value})}
              required            
          />
          <Button icon="cross" onClick={this.resetForm} text="Cancel" />
          <Button type="submit" icon="floppy-disk" text="Save Note" />
        </form>
        
        <h3>Notes</h3>
        <table>
          <tbody>
            {this.props.notes.map((note, id) => (
              <tr key={`note_${id}`}>
                <td>{note.id}</td>
                <td>{note.text}</td>
                <td><button onClick={() => this.selectForEdit(id)}>edit</button></td>
                <td><button onClick={() => this.props.deleteNote(id)}>delete</button></td>
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