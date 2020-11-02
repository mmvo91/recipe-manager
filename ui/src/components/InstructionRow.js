import React from 'react';
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

const instruction = {
    step: 1,
    instruction: ""
};

const InstructionRow = ({instructions, setInstructions}) => {
    const addInstruction = () => {
        let newInstruction = Object.assign({}, instruction);
        newInstruction.step = instructions.length + 1;

        setInstructions(instructions.concat(newInstruction));
    };

    const changeInstruction = idx => event => {
        const updateInstruction = instructions.map(
            (instruction, sidx) => {
                if (idx !== sidx) return instruction;
                return {...instruction, [event.target.name]: event.target.value};
            });

        setInstructions(updateInstruction)
    };

    const removeInstruction = idx => () => {
        setInstructions(instructions.filter((s, sidx) => idx !== sidx))
    };

    return (
        <div className="py-3">
            <h5>Instructions</h5>
            {
                instructions.map(
                    (instruction, idx) => (
                        <Form.Row>
                            <Form.Group className="py-1">
                                <h4 className="my-0">{instruction.step + '. '}</h4>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Control
                                    id={'instruction_' + idx}
                                    name={'instruction'}
                                    value={instruction.instruction}
                                    type="text"
                                    placeholder="Instruction"
                                    onChange={changeInstruction(idx)}
                                />
                            </Form.Group>
                            <Form.Group>
                                <Button variant='danger' onClick={removeInstruction(idx)}>
                                    <FontAwesomeIcon icon={"trash"}/>
                                </Button>
                            </Form.Group>
                        </Form.Row>
                    )
                )
            }
            <div className="text-center">
                <Button onClick={addInstruction}>
                    Add Instruction
                </Button>
            </div>
        </div>
    )
};

export default InstructionRow;