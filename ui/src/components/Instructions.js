import React from "react";

const Instructions = (props) => {
    return (
        <div>
            <h5>Instructions</h5>
            <ol>
                {
                    props.instructions.map(instruction => {
                        return <li key={instruction.step}>{instruction.instruction}</li>
                    })
                }
            </ol>
        </div>
    )
};

Instructions.defaultProps = {
    instructions: []
}

export default Instructions;