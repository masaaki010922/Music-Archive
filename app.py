import streamlit as st
from google import genai

st.title("私のAIアプリ")

# 秘密の鍵を読み込む
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# 【ここが重要！】AI Studioの「System Instructions」を以下に貼り付けます
# ---------------------------------------------------------
my_instruction = """

import React, { useState, useEffect, useMemo } from 'react';
import { Album, SortField, SortOrder } from './types';
import AlbumForm from './components/AlbumForm';
import StatsDashboard from './components/StatsDashboard';
import ComparisonTool from './components/ComparisonTool';
import { 
  Plus, 
  Search, 
  LayoutGrid, 
  List as ListIcon, 
  BarChart3, 
  ArrowUpDown, 
  Trash2, 
  Edit2, 
  Music,
  Scale,
  Info,
  Globe
} from 'lucide-react';

const App: React.FC = () => {
  const [albums, setAlbums] = useState<Album[]>(() => {
    const saved = localStorage.getItem('vibe_archive_albums');
    return saved ? JSON.parse(saved) : [];
  });
  
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'stats'>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortField, setSortField] = useState<SortField>('addedAt');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingAlbum, setEditingAlbum] = useState<Album | undefined>();
  const [selectedForComparison, setSelectedForComparison] = useState<string[]>([]);
  const [isComparing, setIsComparing] = useState(false);

  useEffect(() => {
    localStorage.setItem('vibe_archive_albums', JSON.stringify(albums));
  }, [albums]);

  const uniqueArtists = useMemo(() => 
    Array.from(new Set(albums.map(a => a.artist))).filter(Boolean).sort(),
    [albums]
  );

  const uniqueLabels = useMemo(() => 
    Array.from(new Set(albums.map(a => a.label))).filter(Boolean).sort(),
    [albums]
  );

  const filteredAndSortedAlbums = useMemo(() => {
    return albums
      .filter(a => 
        a.artist.toLowerCase().includes(searchQuery.toLowerCase()) || 
        a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.country?.toLowerCase().includes(searchQuery.toLowerCase())
      )
      .sort((a, b) => {
        const factor = sortOrder === 'asc' ? 1 : -1;
        const valA = a[sortField] || '';
        const valB = b[sortField] || '';
        if (typeof valA === 'string' && typeof valB === 'string') {
          return factor * valA.localeCompare(valB);
        }
        return factor * ((valA as number) - (valB as number));
      });
  }, [albums, searchQuery, sortField, sortOrder]);

  const handleAddAlbum = (album: Album) => {
    if (editingAlbum) {
      setAlbums(prev => prev.map(a => a.id === album.id ? album : a));
    } else {
      setAlbums(prev => [...prev, album]);
    }
    setIsFormOpen(false);
    setEditingAlbum(undefined);
  };

  const handleDelete = (id: string) => {
    if (confirm('本当にこのアルバムを削除しますか？')) {
      setAlbums(prev => prev.filter(a => a.id !== id));
      setSelectedForComparison(prev => prev.filter(i => i !== id));
    }
  };

  const toggleComparison = (id: string) => {
    setSelectedForComparison(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 p-2 rounded-lg text-white shadow-lg shadow-indigo-100">
              <Music size={20} />
            </div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight hidden sm:block">Album Archive</h1>
          </div>

          <div className="flex-1 max-w-md mx-8 relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text"
              placeholder="アーティスト、アルバム、国で検索..."
              className="w-full pl-10 pr-4 py-2 bg-slate-100 border-transparent focus:bg-white focus:ring-2 focus:ring-indigo-500 rounded-xl outline-none transition-all"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="flex items-center gap-2">
             <button 
              onClick={() => { setEditingAlbum(undefined); setIsFormOpen(true); }}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 font-semibold transition-all shadow-lg shadow-indigo-200"
            >
              <Plus size={20} />
              <span className="hidden sm:inline">Add Album</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8">
        {/* Toolbar */}
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between mb-8">
          <div className="flex p-1 bg-white border rounded-xl shadow-sm">
            <button 
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-slate-100 text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}
            >
              <LayoutGrid size={20} />
            </button>
            <button 
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-slate-100 text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}
            >
              <ListIcon size={20} />
            </button>
            <button 
              onClick={() => setViewMode('stats')}
              className={`p-2 rounded-lg transition-colors ${viewMode === 'stats' ? 'bg-slate-100 text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}
            >
              <BarChart3 size={20} />
            </button>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <ArrowUpDown size={16} />
              <select 
                className="bg-transparent border-none outline-none font-medium cursor-pointer"
                value={sortField}
                onChange={e => setSortField(e.target.value as SortField)}
              >
                <option value="addedAt">追加日順</option>
                <option value="artist">アーティスト順</option>
                <option value="title">タイトル順</option>
                <option value="releaseYear">リリース年順</option>
                <option value="country">国順</option>
              </select>
              <button 
                onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
                className="px-2 hover:bg-slate-100 rounded"
              >
                {sortOrder === 'asc' ? '昇順' : '降順'}
              </button>
            </div>

            {selectedForComparison.length > 0 && (
              <button 
                onClick={() => setIsComparing(true)}
                className="flex items-center gap-2 px-4 py-2 bg-violet-50 text-violet-600 border border-violet-100 rounded-xl hover:bg-violet-100 transition-all text-sm font-bold"
              >
                <Scale size={18} />
                比較 ({selectedForComparison.length})
              </button>
            )}
          </div>
        </div>

        {/* Content Views */}
        {viewMode === 'stats' ? (
          <StatsDashboard albums={albums} />
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredAndSortedAlbums.map(album => (
              <div key={album.id} className="group bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden relative">
                <div className="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                  <button 
                    onClick={() => { setEditingAlbum(album); setIsFormOpen(true); }}
                    className="p-2 bg-white/90 backdrop-blur rounded-lg text-slate-600 hover:text-indigo-600 shadow-sm"
                  >
                    <Edit2 size={16} />
                  </button>
                  <button 
                    onClick={() => handleDelete(album.id)}
                    className="p-2 bg-white/90 backdrop-blur rounded-lg text-slate-600 hover:text-rose-600 shadow-sm"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>

                <div className="aspect-square bg-slate-100 flex items-center justify-center relative overflow-hidden">
                  {album.coverUrl ? (
                    <img src={album.coverUrl} alt={album.title} className="w-full h-full object-cover" />
                  ) : (
                    <div className="text-slate-300">
                      <Music size={64} strokeWidth={1} />
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent flex flex-col justify-end p-4">
                    <span className="text-white/70 text-xs font-bold uppercase tracking-wider">{album.artist}</span>
                    <h3 className="text-white font-bold text-lg leading-tight line-clamp-1">{album.title}</h3>
                  </div>
                </div>

                <div className="p-4">
                  <div className="flex items-center justify-between text-xs text-slate-500 font-medium mb-1">
                    <div className="flex items-center gap-1">
                      <Globe size={12} className="text-slate-400" />
                      <span>{album.country || '-'}</span>
                    </div>
                    <span>{album.releaseYear} • {album.label || '-'}</span>
                  </div>
                  <div className="mt-2">
                    <label className="flex items-center gap-1 cursor-pointer text-xs font-medium text-slate-400 hover:text-indigo-600">
                      <input 
                        type="checkbox"
                        className="rounded"
                        checked={selectedForComparison.includes(album.id)}
                        onChange={() => toggleComparison(album.id)}
                      />
                      Compare
                    </label>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white border rounded-2xl overflow-hidden shadow-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b text-slate-500 text-xs uppercase font-bold">
                  <th className="px-6 py-4">Title / Artist</th>
                  <th className="px-6 py-4">Year</th>
                  <th className="px-6 py-4">Country</th>
                  <th className="px-6 py-4">Label</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredAndSortedAlbums.map(album => (
                  <tr key={album.id} className="border-b last:border-0 hover:bg-slate-50/80 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-slate-100 rounded flex items-center justify-center text-slate-400 flex-shrink-0 overflow-hidden">
                           {album.coverUrl ? (
                              <img src={album.coverUrl} className="w-full h-full object-cover" />
                           ) : (
                              <Music size={16} />
                           )}
                        </div>
                        <div>
                          <p className="font-bold text-slate-800 leading-none mb-1">{album.title}</p>
                          <p className="text-xs text-slate-500 font-medium">{album.artist}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-600">{album.releaseYear}</td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-600">
                      <div className="flex items-center gap-1">
                        <Globe size={14} className="text-slate-400" />
                        {album.country || '-'}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-600">{album.label || '-'}</td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                         <button 
                          onClick={() => { setEditingAlbum(album); setIsFormOpen(true); }}
                          className="p-2 hover:text-indigo-600"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button 
                          onClick={() => handleDelete(album.id)}
                          className="p-2 hover:text-rose-600"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {filteredAndSortedAlbums.length === 0 && (
          <div className="text-center py-32">
            <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-400">
              <Search size={32} />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-2">
              {searchQuery ? '検索結果が見つかりませんでした' : 'コレクションが空です'}
            </h3>
            <p className="text-slate-500">
              {searchQuery ? '別のキーワードで試してみてください。' : '右上のボタンから最初のアルバムを追加しましょう！'}
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col md:flex-row items-center justify-between text-slate-400 text-sm gap-4">
          <div className="flex items-center gap-2">
            <Music size={16} />
            <span className="font-bold text-slate-600">Album Archive</span>
            <span>&copy; 2024 Your Music Database</span>
          </div>
          <div className="flex items-center gap-6">
            <a href="#" className="hover:text-slate-600 transition-colors">利用規約</a>
            <a href="#" className="hover:text-slate-600 transition-colors">プライバシー</a>
            <a href="#" className="hover:text-slate-600 transition-colors flex items-center gap-1">
              <Info size={14} /> ヘルプ
            </a>
          </div>
        </div>
      </footer>

      {/* Modals */}
      {isFormOpen && (
        <AlbumForm 
          onSave={handleAddAlbum} 
          onClose={() => { setIsFormOpen(false); setEditingAlbum(undefined); }} 
          initialData={editingAlbum}
          artistSuggestions={uniqueArtists}
          labelSuggestions={uniqueLabels}
        />
      )}

      {isComparing && (
        <ComparisonTool 
          selectedAlbums={albums.filter(a => selectedForComparison.includes(a.id))}
          onRemove={id => setSelectedForComparison(prev => prev.filter(i => i !== id))}
          onClose={() => setIsComparing(false)}
        />
      )}
    </div>
  );
};

export default App;

"""
# ---------------------------------------------------------

user_input = st.text_input("AIに聞きたいことを入力してね")

if st.button("送信"):
    if user_input:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={'system_instruction': my_instruction},
            contents=user_input
        )
        st.write(response.text)
    else:
        st.warning("何か文字を入力してください")
