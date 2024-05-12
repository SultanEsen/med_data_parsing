import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

const LangSwitches = () => {
  return (
      <Tabs defaultValue="en">
        <TabsList>
          <TabsTrigger value="en">EN</TabsTrigger>
          <TabsTrigger value="ru">RU</TabsTrigger>
        </TabsList>
      </Tabs>
  )
}

export default LangSwitches
