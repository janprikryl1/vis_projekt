import {FC} from "react";
import {Card} from "react-bootstrap";
import {Link} from "react-router-dom";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {NewTestType} from "../utils/types/NewTestType.ts";

type Props = {
    test: NewTestType;
}

export const TestCard:FC<Props> = ({test}) => {
    const {user} = useUserContext();

    return (
        <div className="col-sm-4 paddingTop">
            <Card>
                <Card.Body>
                    <Card.Title><Link to={`${user?.type === "student" ? `/test` : '/new_test'}/${test.test_id}`} className="underline-none">{test.title}</Link></Card.Title>
                    <Card.Text>
                        {test.description}
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    )
}
