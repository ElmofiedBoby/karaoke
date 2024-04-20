import type { MetaFunction } from "@remix-run/node";
import Home from "~/components/home";
import LibraryComponent from "~/components/libraryComponent";
import Navbar from "~/components/navbar";

export const meta: MetaFunction = () => {
  return [
    { title: "Karaoke | Library" },
    { name: "description", content: "Karaoke Library" },
  ];
};

export default function Library() {
  return (<>
  
        <Navbar/>
        <LibraryComponent/>
      </>
  );
}
