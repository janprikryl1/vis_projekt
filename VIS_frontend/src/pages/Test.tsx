import {FC, useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import {TestType} from "../utils/types/TestType.ts";
import {getTest} from "../api/testService.ts";
import {TestSkeleton} from "../components/TestSkeleton.tsx";
import {Button} from "react-bootstrap";

export const Test:FC = () => {
    const {id} = useParams();
    const [test, setTest] = useState<TestType>();

    useEffect(() => {
        if (!id) return;
        const getTestDetails = async () => {
            try {
                const result = await getTest(id);
                setTest(result.data);
            } catch (e) {
                console.error(e);
            }
        }
        getTestDetails();
    }, [id]);

    return (
        <div className="container paddingTop">
            {test ? (
                <div>
                    <h1>{test.title}</h1>
                    <h2>{test.subject}</h2>
                    <p>{test.description}</p>
                    <br />
                    <p>Vytvoření: {test.datetime}</p>
                    <p>Test {test.sequence ? "je skevenční" : "není sekvenční"}</p>
                    <Button>Začít vyplňovat</Button>
                </div>
            ) : <TestSkeleton />}
        </div>
    )
}
