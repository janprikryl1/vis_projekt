import {
    createContext,
    useContext,
    useState,
    useEffect,
    ReactNode,
    FC,
    ChangeEventHandler,
    ChangeEvent,
    MouseEventHandler, Dispatch, SetStateAction
} from 'react';
import {useParams} from "react-router-dom";
import {NewTestType} from "../types/NewTestType.ts";
import {getTest, uploadNewTest} from "../../api/testService.tsx";
import { v4 as uuidv4 } from "uuid";

type NewArticleContextType = {
    test: NewTestType;
    setTest: Dispatch<SetStateAction<NewTestType>>;
    handleChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
    handleSubmit: (e: React.MouseEvent<HTMLButtonElement>) => void;
    currentQuestionIndex: number;
    setCurrentQuestionIndex: Dispatch<SetStateAction<number>>;
}

const NewArticleContext = createContext<NewArticleContextType | undefined>(undefined);

export const NewTestProvider: FC<{ children: ReactNode }> = ({ children }) => {
    const { id } = useParams();
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [test, setTest] = useState<NewTestType>({
        test_title: "",
        description: "",
        subject: "",
        date_time: "",
        sequence: false,
        questions: [{
            id: uuidv4(),
            title: "",
            description: "",
            task: "",
            corrects: [],
            show_correct: true,
        }]
    });

    useEffect(() => {
        if (!id) return;
        const getTestDetails = async () => {
            try {
                const result = await getTest(id);
                setTest(result.data);
            } catch (e) {
                console.error(e);
            }
        };
        getTestDetails();
    }, [id]);

    const handleChange: ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement> = (e) => {
        // @ts-ignore
        const { name, value, type, checked } = e.target;
        setTest((prevTest) => ({
            ...prevTest,
            [name]: type === "checkbox" ? checked : value,
        }));
    };

    const handleSubmit: MouseEventHandler<HTMLButtonElement> = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("test_title", test.test_title);
        formData.append("description", test.description);
        formData.append("subject", test.subject);
        formData.append("sequence", test.sequence.toString());
        if (test.max_time) formData.append("max_time", test.max_time.toString());
        formData.append("questions", JSON.stringify(test.questions));

        try {
            const result = await uploadNewTest(formData);
            if (result.status === 200) {

            }
        } catch (e) {
            console.error(e);
        }
    };

    const value: NewArticleContextType = {
        test,
        setTest,
        handleChange,
        handleSubmit,
        currentQuestionIndex,
        setCurrentQuestionIndex
    }

    return (
        <NewArticleContext.Provider value={value}>{children}</NewArticleContext.Provider>
    );
};

export const useNewArticleContext = () => {
    const context = useContext(NewArticleContext);
    if (!context) {
        throw new Error('useNewArticleContext must be used within a NewArticleProvider');
    }
    return context;
};
