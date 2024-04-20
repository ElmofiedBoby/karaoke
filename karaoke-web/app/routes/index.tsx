import type { MetaFunction } from "@remix-run/node";
import Home from "~/components/home";
import Layout from "~/components/layout";
import Navbar from "~/components/navbar";

export const meta: MetaFunction = () => {
  return [
    { title: "Karaoke" },
    { name: "description", content: "Welcome to the open-source karaoke solution!" },
  ];
};

export default function index() {
  return (<>
  
        <Navbar/>
        <Home/>
      </>
  );
}
