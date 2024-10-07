import { FC } from "react";
import { Card } from "react-bootstrap";
import Skeleton from "react-loading-skeleton";

export const TestCardSkeleton: FC = () => {
    return (
        <div className="col-sm-4 paddingTop">
            <Card>
                <Card.Body>
                    <Card.Title>
                        <Skeleton width={150} height={20} />
                    </Card.Title>
                    <Card.Text>
                        <Skeleton count={3} />
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    );
};
