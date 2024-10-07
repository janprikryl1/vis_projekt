import {FC} from "react";
import Skeleton from "react-loading-skeleton";

export const TestSkeleton:FC = () => {
    return (
        <>
        <Skeleton width={850} height={50} />
            <br />
            {Array.from({length:8}).map((_, index) => (
                <Skeleton width={500} height={30} key={index} className="paddingTop"/>
            ))}
        </>
    )
}
