import {FC} from "react";
import {Card} from "react-bootstrap";
import {Link} from "react-router-dom";
import {TestType} from "../utils/types/TestType.ts";

type Props = {
    test: TestType;
}

export const TestCard:FC<Props> = ({test}) => {
    return (
        <div className="col-sm-4 paddingTop">
            <Card>
                <Card.Body>
                    <Card.Title><Link to={`/test/`+test.test_id} className="underline-none">{test.title}</Link></Card.Title>
                    <Card.Text>
                        {test.description}
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    )
}
