import {FC} from "react";
import {Card} from "react-bootstrap";
import {Link} from "react-router-dom";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {NewTestType} from "../utils/types/NewTestType.ts";
import {LatestTestsType} from "../utils/types/LatestTestsType.ts";

type Props = {
    test: NewTestType | LatestTestsType;
}

export const TestCard:FC<Props> = ({test}) => {
    const {user} = useUserContext();

    return (
        <div className="col-sm-4 paddingTop">
            <Card>
                <Card.Body>
                    <Card.Title><Link to={`${user?.user_type === "Pupil" ? `/test` : '/new_test'}/${test.test_id}`} className="underline-none">{"title" in test ? test.title : test.test_title}</Link></Card.Title>
                    <Card.Text>
                        {"description" in test ? test.description : test.created_at}
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    )
}
