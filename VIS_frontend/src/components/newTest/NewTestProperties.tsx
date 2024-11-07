import {FC, useState} from "react";
import {useNewArticleContext} from "../../utils/providers/NewTestProvider.tsx";
import {NewTestInput} from "./NewTestInput.tsx";
import {NewTestCheckBox} from "./NewTestCheckBox.tsx";
import {Button} from "react-bootstrap";

export const NewTestProperties:FC = () => {
    const {test, handleChange} = useNewArticleContext();
    const [showMaxTime, setShowMaxTime] = useState(false);

    return (
        <>
            <h1>Nový test</h1>
            <NewTestInput value={test.test_title} name="test_title" placeholder="Název testu" onChange={handleChange} />
            <NewTestInput value={test.subject} name="subject" placeholder="Předmět" onChange={handleChange} />
            <NewTestInput value={test.description} name="description" placeholder="Popis" onChange={handleChange} />
            <NewTestCheckBox name="sequence" value={test.sequence} title="Sekvenční test" onChange={handleChange} />
            {showMaxTime ? <NewTestInput value={test.max_time ?? 0} name="max_time" placeholder="Maximální čas (s)" type="number" onChange={handleChange} /> : <Button onClick={() => setShowMaxTime(true)}>Maximální čas</Button>}
        </>
    )
}
