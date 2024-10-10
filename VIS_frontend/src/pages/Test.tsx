import {FC, useEffect, useState} from "react";
import {Link, useParams} from "react-router-dom";
import {TestType} from "../utils/types/TestType.ts";
import {getTest} from "../api/testService.ts";
import {TestSkeleton} from "../components/TestSkeleton.tsx";
import {toCzechDateFormat} from "../utils/constants";

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
                    <div className="container" style={{marginTop: 20}}>
                        <div className="row">
                            <div className="col-sm-8">
                                <h1>{test.test.title}</h1>
                                <h2>{test.test.subject}</h2>
                                <h3 style={{whiteSpace: "pre-line"}}>{test.test.description}</h3>
                                <p>Test {test.test.sequence ? "je skevenční" : "není sekvenční"}</p>
                                <p>Vyplněno: {toCzechDateFormat(test.date_time_filled)}</p>
                                <p>Dokončeno na {test.questions.length / test.test.questions.length * 100} %</p>
                        </div>
                        <div className="col-sm-8">
                            <div className="row">
                                <h3>Seznam úkolů v lekci</h3>
                                {test?.questions && test.questions.length > 0 ? test.questions.map((question, index) => (
                                    <div className="col-sm-8" key={index}>
                                        <div className="row">
                                            <div className="col-sm-4">
                                                <Link to={`/question/${question.id}/${question.question.id}`}>{question.question.title}</Link>
                                            </div>
                                            <div className="col-sm-4">
                                            {question.is_correct ? (
                                                <p style={{color: "green"}}>Úspěšně vyplněno</p>
                                            ) : (
                                                <p style={{color: "green"}}>Nevyplněno</p>
                                            )}
                                            </div>
                                        </div>
                                    </div>
                                )) : <h3>Žádné otázky v testu</h3>}
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            ) : <TestSkeleton />}
        </div>
    )
}
