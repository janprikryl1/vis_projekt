import {FC} from "react";
import Form from "react-bootstrap/Form";

type Props = {
    value: string | number;
    name: string;
    placeholder: string;
    type?: 'string' | 'number';
    onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
}

export const NewTestInput:FC<Props> = ({value, placeholder, name, type = "text", onChange}) => {
    return (
        <Form.Group className="mb-3">
            <Form.Label>{placeholder}</Form.Label>
            <Form.Control
                type={type}
                placeholder={`${placeholder}...`}
                value={value}
                name={name}
                onChange={onChange}
            />
        </Form.Group>
    )
}
