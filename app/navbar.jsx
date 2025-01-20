import Link from 'next/link'

export default function Navbar(){
    return(
        <nav> 
            <h1>Menu</h1> 

            <ul>
                <li> 
                    <Link href="/"> Home </Link>
                </li>
                <li> 
                    <Link href="/src/about"> About </Link>
                </li>
                <li> 
                    <Link href="/src/Proteinas"> Proteinas </Link>
                </li>
            </ul>
        </nav> 
    );
}