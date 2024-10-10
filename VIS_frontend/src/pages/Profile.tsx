import {FC, useState} from "react";
import {Button} from "react-bootstrap";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {useNavigate} from "react-router-dom";
import {saveUserDetails} from "../api/userService.ts";
import {UserType} from "../utils/types/UserType.ts";
import {TestCard} from "../components/TestCard.tsx";

export const Profile:FC = () => {
    const {user, setUser} = useUserContext();
    const navigate = useNavigate();
    if (!user) navigate("/");

    const [editedUser, setEditedUser] = useState<UserType>(user!);
    const [lastTests, setLastTests] = useState([]);

    const saveUserChanges = () => {
        saveUserDetails(editedUser!);
        setUser(editedUser);
    }


    return (
        <div className="container">
            <div style={{marginTop: "20px"}}>
                <h1>Vítejte zpět, { user!.first_name }</h1>
            </div>
            <div>
                <h2>Detaily uživatele</h2>
                <input type="text" value={user!.first_name} onChange={(e) => setEditedUser({...editedUser, first_name: e.target.value})}/>
                <input type="text" value={user!.last_name} onChange={(e) => setEditedUser({...editedUser, last_name: e.target.value})}/>
                <Button onClick={saveUserChanges}>Uložit změny</Button>
            </div>
            <div className="row">
                <h3>Moje poslední testy</h3>
                <div className="row row-cols-1 row-cols-lg-3 align-items-stretch g-4 py-5" style={{marginTop: -15, marginLeft: "0.1%"}}>
                    {lastTests.map((test)=> (
                        <div className="col">
                            <TestCard test={test} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
