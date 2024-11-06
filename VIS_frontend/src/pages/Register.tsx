import {ChangeEventHandler, FC, FormEventHandler, useEffect, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import Swal from "sweetalert2";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {register} from "../api/userService.ts";
import {registerUserType} from "../utils/types/registerUserType.ts";
import {LoginRegisterInput} from "../components/LoginRegisterInput.tsx";


export const Register: FC = () => {
    const navigate = useNavigate();
    const { setUser, user } = useUserContext();

    useEffect(() => {
        if (user) navigate("/profile");
    }, [user]);

    const [registerData, setRegisterData] = useState<registerUserType>({
        name: "",
        surname: "",
        email: "",
        password: "",
    });

    const handleChange: ChangeEventHandler<HTMLInputElement> = (e) => {
        setRegisterData({ ...registerData, [e.target.name]: e.target.value });
    };

    const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
        e.preventDefault();
        try {
            const response = await register(registerData);

            if (response.data.status === "error") {
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: response.data.status,
                });
            } else {
                Swal.fire({
                    icon: "success",
                    title: "Registrace proběhla úspěšně",
                }).then(() => {
                    setUser(response.data);
                    navigate("/");
                });
            }
        } catch (error) {
            console.error(error);
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Při registraci nastala chyba",
            });
        }
    };

    return (
        <>
            <section className="account padding-top padding-bottom">
                <div className="container">
                    <div
                        className="account__wrapper"
                        data-aos="fade-up"
                        data-aos-duration="800"
                    >
                        <div className="row g-4">
                            <div className="col-12">
                                <div className="account__content account__content--style1">
                                    <div className="account__header">
                                        <h2>Vytvořit profil</h2>
                                    </div>
                                    <form onSubmit={handleSubmit}>
                                        <LoginRegisterInput handleChange={handleChange} placeholder="Jméno"
                                                            name="name" required/>
                                        <LoginRegisterInput handleChange={handleChange} placeholder="Přijmení"
                                                            name="surname" required/>
                                        <LoginRegisterInput handleChange={handleChange} placeholder="Email" name="email"
                                                            type="email" required/>
                                        <LoginRegisterInput handleChange={handleChange} placeholder="Heslo"
                                                            name="password" type="password" required/>
                                        <div className="d-flex justify-content-center mt-4">
                                            <button className="btn btn-outline-warning btn-block btn-lg gradient-custom-4 text-body">Registrovat</button>
                                        </div>
                                    </form>

                                    <div className="account__switch">
                                        <p>
                                            Máte už profil?<Link to={"/login"} className="link-underline-none">Login</Link>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </>
    );
};
