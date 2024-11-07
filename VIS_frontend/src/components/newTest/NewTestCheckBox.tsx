import {FC} from "react";
import Form from "react-bootstrap/Form";

type Props = {
    value: boolean;
    name: string;
    title: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
}

export const NewTestCheckBox:FC<Props> = ({value, name, title, onChange}) => {
    return (
        <Form.Group controlId="formFile" className="mb-3">
            <Form.Label>{title}</Form.Label>
            <Form.Check
                type="checkbox"
                label="Ano"
                checked={value}
                onChange={onChange}
                name={name}
            />
        </Form.Group>
    )
}
