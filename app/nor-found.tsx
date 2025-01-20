// Para cuando la pagina da un error 404

import Link from 'next/link'

export default function NotFound(){
    return (
        <section>
            <h1>404</h1>
            <p> Página no encontrada </p>
            <Link href= "/"> Volver </Link>
        </section>
    )
}