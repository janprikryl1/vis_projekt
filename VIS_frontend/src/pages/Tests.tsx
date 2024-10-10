import {FC, useEffect, useState} from "react";
import {getAllTest} from "../api/testService.ts";
import {TestCard} from "../components/TestCard.tsx";
import {TestCardSkeleton} from "../components/TestCardSkeleton.tsx";
import {NewTestType} from "../utils/types/NewTestType.ts";

export const Tests:FC = () => {
    const [tests, setTests] = useState<NewTestType[]>();

    useEffect(() => {
        const getTests = async () => {
            try {
                const result = await getAllTest();
                setTests(result.data);
            } catch (e) {
                console.error(e);
            }
        }
        getTests();
    }, []);



    return (
        <div className="container">
            <h1>Testy</h1>
            <div className="row">
            {tests && tests.length > 0 ? (
                tests.map((test, index) => (
                    <TestCard key={index} test={test} />
                ))
            ) : Array.from({ length: 9 }).map((_, index) => (
                <TestCardSkeleton key={index} />
            ))}
            </div>
        </div>
    )
}
