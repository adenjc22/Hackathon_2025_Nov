/**
 * Analytics and monitoring utilities
 * Tracks user interactions and performance metrics
 */

// Simple event tracking (can be extended with Google Analytics, Mixpanel, etc.)
export const trackEvent = (eventName, properties = {}) => {
  if (typeof window !== "undefined") {
    console.log(`[Analytics] ${eventName}`, properties);
    
    // TODO: Add integration with analytics service
    // Example: window.gtag?.('event', eventName, properties);
    // Example: window.mixpanel?.track(eventName, properties);
  }
};

// Track search events
export const trackSearch = (query, searchType, resultsCount) => {
  trackEvent("search_performed", {
    query,
    search_type: searchType,
    results_count: resultsCount,
    timestamp: new Date().toISOString(),
  });
};

// Track filter usage
export const trackFilterUsage = (filterType, filterValue) => {
  trackEvent("filter_applied", {
    filter_type: filterType,
    filter_value: filterValue,
    timestamp: new Date().toISOString(),
  });
};

// Track result interaction
export const trackResultClick = (mediaId, position, score) => {
  trackEvent("search_result_clicked", {
    media_id: mediaId,
    position,
    relevance_score: score,
    timestamp: new Date().toISOString(),
  });
};

// Performance monitoring
export const measurePerformance = (metricName, callback) => {
  const startTime = performance.now();
  
  try {
    const result = callback();
    
    // If it's a promise, wait for it
    if (result instanceof Promise) {
      return result.finally(() => {
        const endTime = performance.now();
        const duration = endTime - startTime;
        
        console.log(`[Performance] ${metricName}: ${duration.toFixed(2)}ms`);
        
        // TODO: Send to monitoring service
        // Example: window.newrelic?.recordMetric(metricName, duration);
      });
    }
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    console.log(`[Performance] ${metricName}: ${duration.toFixed(2)}ms`);
    
    return result;
  } catch (error) {
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    console.error(`[Performance] ${metricName} failed after ${duration.toFixed(2)}ms:`, error);
    throw error;
  }
};

// Error logging
export const logError = (error, context = {}) => {
  console.error("[Error]", error, context);
  
  // TODO: Send to error tracking service
  // Example: Sentry.captureException(error, { extra: context });
};

// Page view tracking
export const trackPageView = (path) => {
  trackEvent("page_view", {
    path,
    timestamp: new Date().toISOString(),
  });
};

// Session tracking
export const getSessionId = () => {
  let sessionId = sessionStorage.getItem("session_id");
  
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(7)}`;
    sessionStorage.setItem("session_id", sessionId);
  }
  
  return sessionId;
};

// User engagement metrics
export const trackEngagement = (action, details = {}) => {
  trackEvent("user_engagement", {
    action,
    session_id: getSessionId(),
    ...details,
    timestamp: new Date().toISOString(),
  });
};
