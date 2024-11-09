import {FC} from "react";
import {useParams} from "react-router-dom";

export const TestStatistics:FC = () => {
    const {id} = useParams();

    return (
        <div>
            <h1>Statistiky</h1>
        </div>
    )
}
