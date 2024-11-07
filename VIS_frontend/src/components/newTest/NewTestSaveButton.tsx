import {FC} from "react";
import {Button} from "react-bootstrap";
import {useNewArticleContext} from "../../utils/providers/NewTestProvider.tsx";

export const NewTestSaveButton:FC = () => {
    const {handleSubmit} = useNewArticleContext();

    return (
        <Button onClick={handleSubmit} variant="success" style={{marginTop: 20}}>Uložit</Button>
    )
}
