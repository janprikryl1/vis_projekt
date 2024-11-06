import {ChangeEventHandler, FC, FormEventHandler, useEffect, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import Swal from "sweetalert2";
import {login} from "../api/userService.ts";
import {useUserContext} from "../utils/providers/UserProvider.tsx";
import {LoginRegisterInput} from "../components/LoginRegisterInput.tsx";
export const SignIn: FC = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "", password: ""
    });
    const {setUser, user} = useUserContext();

    useEffect(() => {
        if (user) navigate("/profile");
    }, [user]);

    const handleChange: ChangeEventHandler<HTMLInputElement> = (e) => {
        setFormData({
            ...formData, [e.target.name]: e.target.value
        });
    }

    const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
        e.preventDefault();
        try {
            const response = await login(formData);
            if (response.data.user_id !== null) {
                Swal.fire({
                    icon: "success", title: "Přihlášení proběhlo úšpěšně", text: "Vítejte zpět!",
                }).then(() => {
                    setUser(response.data);
                    navigate("/profile");
                });
            } else {
                Swal.fire({
                    icon: "error", title: "Přihlášení selhalo", text: "Neplatná emailová adresa nebo heslo. Zkuste to prosím znovu.",
                });
            }
        } catch (error) {
            console.error(error);
            Swal.fire({
                icon: "error", title: "Přihlášení selhalo", text: "Neplatná emailová adresa nebo heslo. Zkuste to prosím znovu.",
            });
        }
    }

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
                                        <h2>Vítejte zpět</h2>
                                    </div>
                                    <form onSubmit={handleSubmit}>
                                        <LoginRegisterInput handleChange={handleChange} placeholder="Email" name="email"
                                                            type="email"/>
                                        <LoginRegisterInput handleChange={handleChange} placeholder="Heslo"
                                                            name="password" type="password"/>
                                        <div className="d-flex justify-content-center mt-4">
                                            <button
                                                className="btn btn-outline-warning btn-block btn-lg gradient-custom-4 text-body">Přihlásit se</button>
                                        </div>
                                    </form>
                                    <div className="account__switch">
                                        <p>
                                            Nemáte ješte profil?<Link to="/register" className="link-underline-none">Registrovat</Link>
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
}
