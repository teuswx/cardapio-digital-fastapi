import styles from "./page.module.scss";
import Image from "next/image"
import Menu from '../../public/Menu.png'
import {api} from "@/services/api"
import {cookies} from "next/headers"
import { redirect } from "next/navigation";
export default function Home() {

  async function handleLogin(formData: FormData){
    "use server"
    const username = formData.get("username")
    const password = formData.get("password")

    if( username === "" || password === ""){
      console.log("deu erro ou no password ou no username")
      return;
    }

    try{
      const response = await api.post("/user/login",formData,{
        headers:{
          'Content-Type': 'multipart/form-data'
        },
      });

      const token = response.data.token

      if(!token){
        console.log("token vazio")
        return;
      }

      const expressTime = 60 * 60 * 24 * 30 * 1000;

      const cookieStore = await cookies();

      cookieStore.set("session", token, {
        maxAge: expressTime,
        path: "/",
        httpOnly: false,
        secure: process.env.NODE_ENV == "production"
      })


    }catch(err){
      console.log(err)
      return;
    }

    redirect('/dashboard')
  }

  return (
    <>
      <div className={styles.containerCenter}>
        <div className={styles.leftSide}>
        <Image
          src={Menu}
          alt="Logo Cardapio Digital"
        />
        </div>

        <section className={styles.login}>
          <form action={handleLogin}>
            <input
              type="text"
              required
              name="username"
              placeholder="Digite seu nome"
              className={styles.input}
            />

            <input
              type="password"
              required
              name="password"
              placeholder="Digite sua senha"
              className={styles.input}
            />

            <button type="submit" className={styles.button}>
              Acessar
            </button>

          </form>

        </section>
      </div>
    </>
  );
}
