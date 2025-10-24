import Map from "./Map";
import ChatContainer from "./chat/ChatContainer";
import QuickClose from "./QuickClose";
// import Listing from "./dropdown/Listing.tsx";
import { NavUser } from "./components/nav-user";

function Home() {
  return (
    <div className="w-screen flex overflow-hidden">
      <NavUser />
      <div className="fixed z-60 top-0 left-0 w-full group justify-center hidden sm:block">
        <div className="flex justify-end px-20 py-2 bg-[#DCEAAB] opacity-0 -translate-y-full transition-all duration-150 ease-in-out pointer-events-none group-hover:opacity-100 group-hover:translate-y-0 group-hover:pointer-events-auto">
          <QuickClose />
        </div>
      </div>
      <div className="absolute z-60 top-3 right-27 block sm:hidden">
        <QuickClose />
      </div>
      <div className="absolute inset-0 z-0">
        <Map />
      </div>
      {/* <div className="absolute inset-0 top-0 left-0 sm:top-10 sm:left-10">
                <Listing/>
            </div> */}
      <div>
        <ChatContainer />
      </div>
    </div>
  );
}

export default Home;
