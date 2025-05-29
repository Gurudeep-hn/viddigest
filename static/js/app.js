// Global variables
let currentVideoData = null;

// DOM elements
const urlInput = document.getElementById('videoUrl');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const resultsSection = document.getElementById('resultsSection');
const analyzeBtn = document.querySelector('.analyze-btn');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus URL input
    urlInput.focus();
    
    // Enter key support
    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            analyzeVideo();
        }
    });
    
    // Clear previous results when input changes
    urlInput.addEventListener('input', function() {
        hideResults();
        hideError();
    });
    
    // Check server health on load
    checkServerHealth();
});

async function checkServerHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (!data.model_loaded) {
            showNotification('Warning: AI model not loaded. Some features may be limited.', 'warning');
        }
    } catch (error) {
        console.warn('Could not check server health:', error);
    }
}

async function analyzeVideo() {
    const url = urlInput.value.trim();
    
    // Validation
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    if (!isValidYouTubeUrl(url)) {
        showError('Please enter a valid YouTube URL');
        return;
    }
    
    // UI state updates
    showLoading();
    hideError();
    hideResults();
    setButtonLoading(true);
    
    try {
        // Make API request
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_url: url
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze video');
        }
        
        const data = await response.json();
        currentVideoData = data;
        
        // Display results
        displayResults(data);
        showResults();
        
        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }, 300);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze video. Please try again.');
    } finally {
        hideLoading();
        setButtonLoading(false);
    }
}

function displayResults(data) {
    // Video info
    document.getElementById('videoTitle').textContent = data.title;
    document.getElementById('videoDuration').textContent = `📅 Duration: ${data.duration}`;
    document.getElementById('videoViews').textContent = `👁️ ${data.views} views`;
    document.getElementById('videoChannel').textContent = `📺 ${data.channel}`;
    
    // Summary
    document.getElementById('summaryContent').textContent = data.summary;
    
    // Key points
    const keyPointsList = document.getElementById('keyPoints');
    keyPointsList.innerHTML = '';
    
    if (data.key_points && data.key_points.length > 0) {
        data.key_points.forEach(point => {
            const li = document.createElement('li');
            li.textContent = point;
            keyPointsList.appendChild(li);
        });
    } else {
        document.getElementById('keyPointsSection').style.display = 'none';
    }
    
    // Timestamps
    const timestampsDiv = document.getElementById('timestamps');
    if (data.timestamps && data.timestamps.length > 0) {
        timestampsDiv.innerHTML = data.timestamps.map(timestamp => 
            `<div style="margin-bottom: 8px;">${timestamp}</div>`
        ).join('');
    } else {
        timestampsDiv.textContent = 'No timestamps available';
    }
}

function copyToClipboard(type) {
    let text = '';
    let button = event.target;
    
    if (type === 'summary') {
        text = document.getElementById('summaryContent').textContent;
    } else if (type === 'timestamps') {
        const timestampsDiv = document.getElementById('timestamps');
        text = timestampsDiv.textContent.replace(/\n\s*\n/g, '\n');
    }
    
    if (!text) {
        showNotification('Nothing to copy', 'error');
        return;
    }
    
    // Use modern clipboard API
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showCopySuccess(button);
        }).catch(() => {
            fallbackCopy(text, button);
        });
    } else {
        fallbackCopy(text, button);
    }
}

function fallbackCopy(text, button) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(button);
    } catch (err) {
        showNotification('Copy failed', 'error');
    }
    
    document.body.removeChild(textArea);
}

function showCopySuccess(button) {
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.classList.add('copied');
    
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('copied');
    }, 2000);
    
    showNotification('Copied to clipboard!', 'success');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 20px',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '1000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Set background color based on type
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function isValidYouTubeUrl(url) {
    const patterns = [
        /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)/,
        /^https?:\/\/(www\.)?youtube\.com\/watch\?.*v=/
    ];
    
    return patterns.some(pattern => pattern.test(url));
}

function showLoading() {
    loadingSection.classList.add('active');
    updateLoadingText();
}

function hideLoading() {
    loadingSection.classList.remove('active');
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.classList.add('active');
}

function hideError() {
    errorSection.classList.remove('active');
}

function showResults() {
    resultsSection.classList.add('active');
}

function hideResults() {
    resultsSection.classList.remove('active');
}

function setButtonLoading(isLoading) {
    const btnText = analyzeBtn.querySelector('.btn-text');
    
    if (isLoading) {
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('loading');
        btnText.textContent = '🔄 Analyzing';
    } else {
        analyzeBtn.disabled = false;
        analyzeBtn.classList.remove('loading');
        btnText.textContent = '🎯 Analyze Video';
    }
}

function updateLoadingText() {
    const messages = [
        'Extracting video information...',
        'Getting transcript data...',
        'Analyzing content with AI...',
        'Generating summary...',
        'Extracting key points...',
        'Almost done...'
    ];
    
    let index = 0;
    const loadingTextElement = document.getElementById('loadingText');
    
    const interval = setInterval(() => {
        if (!loadingSection.classList.contains('active')) {
            clearInterval(interval);
            return;
        }
        
        loadingTextElement.textContent = messages[index];
        index = (index + 1) % messages.length;
    }, 2000);
}

// Utility functions
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function formatViews(views) {
    const num = parseInt(views);
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}