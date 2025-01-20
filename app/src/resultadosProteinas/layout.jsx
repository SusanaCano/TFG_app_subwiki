
import Navbar from "../../../components/navigation";
import Footer from "../../../components/Footer";

export default function Layout({ children }) {
  return (
    <>
      <Navbar />
      <main className="is-flex is-flex-direction-column is-align-items-center is-justify-content-center">
        {children}
      </main>
      <Footer />
    </>
  );
}
