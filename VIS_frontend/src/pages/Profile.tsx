import {FC, useEffect, useState} from "react";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {useNavigate} from "react-router-dom";
import {TestCard} from "../components/TestCard.tsx";
import {Button} from "react-bootstrap";
import {getLatestTest} from "../api/testService.ts";
import {LatestTestsType} from "../utils/types/LatestTestsType.ts";
import {v4 as uuidv4} from 'uuid';

export const Profile:FC = () => {
    const {user, logout} = useUserContext();
    const navigate = useNavigate();
    const [lastTests, setLastTests] = useState<LatestTestsType[]>();
    if (!user) navigate("/");

    useEffect(() => {
        const loadLatestTests = async () => {
            try {
                const result = await getLatestTest();
                setLastTests(result.data.latest_tests);
            } catch (e) {
                console.error(e);
            }
        }
        loadLatestTests();
    }, []);


    return (
        <>
            {user ? (
            <div className="container">
                <div style={{marginTop: "20px"}}>
                    <h1>Vítejte zpět, { user.name }</h1>
                </div>
                <div>
                    <h2>Detaily uživatele</h2>
                    <p>Jméno: {user.name}</p>
                    <p>Přijmení: {user.surname}</p>
                    <p>Email: {user.email}</p>
                    <p>Typ: {user.user_type}</p>
                    <Button variant="warning" onClick={logout}>Odhlásit se</Button>
                </div>
                <div className="row">
                    <h3>Moje poslední testy</h3>
                    <div className="row row-cols-1 row-cols-lg-3 align-items-stretch g-4 py-5" style={{marginTop: -15, marginLeft: "0.1%"}} key={uuidv4()}>
                        {lastTests === undefined ? (
                            <p>Načítání posledních testů</p>
                        ) : lastTests.length === 0 ? (
                            <p>Žádné poslední testy</p>
                        ) : lastTests.map((test)=> (
                            <div className="col">
                                <TestCard test={test} />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
                ) : <p>Načítání</p>}
        </>
    )
}
