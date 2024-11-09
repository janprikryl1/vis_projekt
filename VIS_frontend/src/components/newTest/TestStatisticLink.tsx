import {FC} from "react";
import {Link, useParams} from "react-router-dom";
import {useNewArticleContext} from "../../utils/providers/NewTestProvider.tsx";

export const TestStatisticLink:FC = () => {
    const { id } = useParams();
    const {test} = useNewArticleContext();

    if (test.test_id) {
        return (
            <div>
                <Link to={`/test-statistics/${id}`}>Statistiky</Link>
            </div>
        )
    }
}
