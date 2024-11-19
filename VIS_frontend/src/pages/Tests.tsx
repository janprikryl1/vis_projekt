import {FC, useEffect, useState} from "react";
import {TestCard} from "../components/TestCard.tsx";
import {TestCardSkeleton} from "../components/TestCardSkeleton.tsx";
import {NewTestType} from "../utils/types/NewTestType.ts";
import {getAllTest} from "../api/testService.ts";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {Link} from "react-router-dom";

export const Tests:FC = () => {
    const {user} = useUserContext();
    const [tests, setTests] = useState<{filled_tests: []; tests: NewTestType[]}>();

    useEffect(() => {
        const getTests = async () => {
            try {
                const result = await getAllTest();
                console.error(result.data)
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
            {user && user.user_type === "Teacher" ? <Link to="/new_test">Přidat test</Link>
            :user?.user_type === "Pupil" && tests && tests.filled_tests && tests.filled_tests.length > 0 && (
                <>
                    <h2>Vyplněné testy</h2>
                    {tests.filled_tests.map((filled_test, index) => (
                        <TestCard key={index} test={filled_test} />
                    ))}
                </>
            )}
            <div className="row">
                <h2>Všechny testy</h2>
                {tests === undefined ?
                Array.from({ length: 9 }).map((_, index) => (
                <TestCardSkeleton key={index} />
            )) : tests.tests.length === 0 ? (
                    <p>Žádné testy</p>
            ) : tests.tests.map((test, index) => (
                <TestCard key={index} test={test} />
            ))}
            </div>
        </div>
    )
}
