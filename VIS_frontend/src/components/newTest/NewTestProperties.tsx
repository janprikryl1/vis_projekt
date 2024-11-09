import {FC} from "react";
import {useNewArticleContext} from "../../utils/providers/NewTestProvider.tsx";
import {NewTestInput} from "./NewTestInput.tsx";
import {NewTestCheckBox} from "./NewTestCheckBox.tsx";

export const NewTestProperties:FC = () => {
    const {test, handleChange} = useNewArticleContext();

    return (
        <>
            <h1>Nový test</h1>
            <NewTestInput value={test.test_title} name="test_title" placeholder="Název testu" onChange={handleChange} />
            <NewTestInput value={test.subject} name="subject" placeholder="Předmět" onChange={handleChange} />
            <NewTestInput value={test.description} name="description" placeholder="Popis" onChange={handleChange} />
            <NewTestCheckBox name="sequence" value={test.sequence} title="Sekvenční test" onChange={handleChange} />
        </>
    )
}
