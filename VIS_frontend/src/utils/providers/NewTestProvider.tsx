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
import {getTest, uploadNewTest} from "../../api/testService.ts";
import { v4 as uuidv4 } from "uuid";
import Swal from "sweetalert2";

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
            task: "",
            help: "",
            corrects: [],
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
        if (test.test_id) formData.append("test_id", test.test_id.toString());
        formData.append("test_title", test.test_title);
        formData.append("description", test.description);
        formData.append("subject", test.subject);
        formData.append("sequence", test.sequence.toString());
        formData.append("questions", JSON.stringify(test.questions));

        try {
            const result = await uploadNewTest(formData);
            if (result.status === 201) {
                Swal.fire({
                    title: test.test_id ? "Test aktualizován" : "Test uložen",
                    icon: "success",
                    showConfirmButton: false,
                });
                setTest((prevTest: NewTestType) => ({
                    ...prevTest,
                    test_id: result.data.test_id,
                }));
                console.log(result.data, test);
            }
        } catch (e) {
            console.error(e);
            Swal.fire({
                title: "Chyba",
                text: "Test se nepodařilo uložit",
                icon: "error",
                showConfirmButton: false,
            });
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
