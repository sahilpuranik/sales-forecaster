import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { UploadPage } from './components/UploadPage';
import { PreviewPage } from './components/PreviewPage';
import { ForecastPage } from './components/ForecastPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('upload');
  
  return (
    <div className="min-h-screen bg-background">
      <div className="border-b bg-card">
        <div className="flex items-center justify-between p-6">
          <h1 className="text-3xl font-bold">Sales Forecaster</h1>
        </div>
      </div>

      <div className="p-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-8">
            <TabsTrigger 
              value="upload" 
              onClick={() => setActiveTab('upload')}
              data-state={activeTab === 'upload' ? 'active' : 'inactive'}
            >
              Upload CSV
            </TabsTrigger>
            <TabsTrigger 
              value="preview" 
              onClick={() => setActiveTab('preview')}
              data-state={activeTab === 'preview' ? 'active' : 'inactive'}
            >
              Diagnostics
            </TabsTrigger>
            <TabsTrigger 
              value="forecast" 
              onClick={() => setActiveTab('forecast')}
              data-state={activeTab === 'forecast' ? 'active' : 'inactive'}
            >
              Results
            </TabsTrigger>
          </TabsList>

          {activeTab === 'upload' && (
            <TabsContent value="upload">
              <UploadPage />
            </TabsContent>
          )}

          {activeTab === 'preview' && (
            <TabsContent value="preview">
              <PreviewPage />
            </TabsContent>
          )}

          {activeTab === 'forecast' && (
            <TabsContent value="forecast">
              <ForecastPage />
            </TabsContent>
          )}
        </Tabs>
      </div>
    </div>
  );
}
