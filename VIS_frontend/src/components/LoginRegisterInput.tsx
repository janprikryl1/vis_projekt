import {ChangeEventHandler, FC} from "react";

type Props = {
    handleChange: ChangeEventHandler<HTMLInputElement>;
    name: string;
    placeholder: string;
    type?: string;
    required?: boolean;
}

export const LoginRegisterInput:FC<Props> = ({handleChange, name, placeholder, type = "text", required = false}) => {
    return (
        <div className="form-outline mb-4">
            <label htmlFor="name" className="form-label">{placeholder}</label>
            <input
                type={type}
                name={name}
                placeholder={placeholder + "..."}
                className="form-control form-control-lg"
                onChange={handleChange}
                required={required}
                minLength={type === "password" ? 6 : 1}
            />
        </div>
    );
};
