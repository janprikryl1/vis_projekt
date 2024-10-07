import {FC} from "react";
import {Button} from "react-bootstrap";
import {Link} from "react-router-dom";

export const NoPage:FC = () => {
    return (
        <div className="center-content">
            <h1>Chyba</h1>
            <p>Tady nic nenajdete!</p>
            <Link to="/"><Button>Domů</Button></Link>
        </div>
    );
}
